# TB2 Orchestrator Scope Development Plan

## Summary

This plan covers only the pieces that should remain in `external-audit-orchestrator`:

- audit packet format
- three-reviewer TB2 request JSON export
- expected reviewer output schema
- normalized audit report merge
- documentation and fallback flow

TB2 runtime execution tools such as `workstream_create`, `reviewer_send`, `reviewer_wait`, `reviewer_read`, and process-spawn diagnostics belong in the TB2 runtime project, not in this skill package.

## Goals

1. Make TB2 mode honest: this skill can export request artifacts now, but live execution requires TB2 runtime tools that may not be exposed in the active MCP surface.
2. Make three-reviewer audit requests repeatable by generating stable reviewer-specific JSON request artifacts.
3. Make reviewer results machine-checkable by defining a JSON-first expected output schema.
4. Make report normalization deterministic enough for rerun and partial-failure workflows.
5. Preserve provenance and redaction policy without storing raw transcript text by default.

## Non-Goals

- Do not implement TB2 runtime MCP tools in this repository.
- Do not call low-level terminal, bridge, room, or pane primitives directly from this skill.
- Do not treat TB2 template export as a completed live audit.
- Do not store raw reviewer transcript text unless an operator explicitly opts into that in the runtime layer.
- Do not inline the full audit packet into TB2 request artifacts by default; use `packet_path` plus `packet_sha256` unless the operator explicitly requests embedded packet transport.

## Implementation Scope

### 1. Documentation

Update the TB2 mode documentation to split the current behavior into two clearly named states:

- `tb2-template-export`: supported by this skill now.
- `tb2-live-review`: requires TB2 runtime tools and must be treated as unavailable unless those tools are present.

Update the install flow to state that generated request JSON is an artifact handoff, not proof that a reviewer ran.

Update same-provider documentation so reviewer output is expected to be JSON-first and invalid output is a failed or partial review, not a successful audit.

### 2. TB2 Request Export

Replace the minimal `codex_relay`-only template with a request contract containing:

- `request_id`
- `workstream_id`
- `correlation_id`
- `reviewer_profile`
- `audit_mode`
- `scope`
- `packet_path`
- `packet_sha256`
- `packet_transport`
- `prompt`
- `expected_output_schema`
- `timeout_seconds`
- `provenance_policy`
- `redaction_policy`

Add support for three reviewer roles:

- `product-process`
- `engineering-test`
- `compatibility-provenance`

The exporter should be able to emit either:

- a single reviewer request when a role is specified, or
- three reviewer request files when no role is specified.

Default request output layout:

```text
.audit/tb2/requests/
  product-process.request.json
  engineering-test.request.json
  compatibility-provenance.request.json
  manifest.json
```

Default result input layout:

```text
.audit/tb2/results/
  product-process.result.json
  engineering-test.result.json
  compatibility-provenance.result.json
  manifest.json
```

ID rules:

- `correlation_id`: generated once per export batch as `audit-<UTC yyyyMMddHHmmss>-<8 hex chars>` unless supplied by the caller for rerun.
- `workstream_id`: defaults to the `correlation_id` and is shared by all reviewer requests in the batch.
- `request_id`: role scoped as `<correlation_id>-<reviewer-role>`.
- rerun preserves `correlation_id` when the caller supplies it, but request IDs remain role scoped.

Packet transport rules:

- default `packet_transport` is `path-reference`; `prompt` tells the runtime/reviewer to read `packet_path` and verify `packet_sha256`.
- optional embedded transport may place the packet body in the prompt or a dedicated packet field, but this is explicit opt-in and should be treated as raw prompt content.

### 3. Expected Output Schema

Define the expected reviewer response as JSON with these required fields:

- `reviewer_id`
- `verdict`
- `findings`
- `assumptions`
- `reference_inputs_used`
- `confidence`
- `requires_rerun`

The normalizer also accepts a result wrapper for timeout, invalid, and failed reviewers:

- `reviewer_id`
- `status`: `completed`, `timeout`, `invalid`, or `failed`
- `result`: reviewer response object or `null`
- `error`: failure message or `null`
- `timed_out`
- `raw_result_path`
- `validated_at`

Each finding should include:

- `severity`
- `title`
- `location`
- `risk`
- `recommended_action`

Allowed severities:

- `Critical`
- `Warning`
- `Suggestion`

Allowed verdicts:

- `accept`
- `fix-and-rerun`
- `escalate-to-human`
- `archive-only`

Required field types:

- `reviewer_id`: string matching the reviewer profile id.
- `findings`: array of finding objects.
- `assumptions`: array of strings.
- `reference_inputs_used`: array of objects with `kind`, `target`, and `reason`.
- `confidence`: number from `0` to `1`.
- `requires_rerun`: boolean.

### 4. Normalized Report Merge

Update the normalizer to try JSON parsing first.

Supported raw review input shapes:

- one JSON reviewer result object
- one JSON result wrapper object
- an array of JSON reviewer result objects
- an array of JSON result wrapper objects
- a directory containing `*.result.json`
- existing Markdown reviewer output as fallback

The normalized report should include:

- audit mode
- scope
- reviewer status summary
- reference inputs
- findings grouped by severity
- assumptions
- disposition
- next action

Disposition defaults:

- all reviewers valid and no warning-or-higher findings: `accept`
- any warning-or-higher finding: `fix-and-rerun`
- any timeout, invalid output, or failed reviewer: `fix-and-rerun`
- explicit severe provenance or safety uncertainty: `escalate-to-human`

### 5. Fallback Flow

If TB2 live tools are not available, the workflow should:

1. build the audit packet
2. export TB2 request artifacts
3. write a clear operator note that live execution was not performed
4. skip normalized report generation unless raw reviewer results are provided

If same-provider review returns invalid output, the workflow should:

1. mark that reviewer invalid
2. avoid `accept`
3. produce or point to TB2/web-manual fallback request artifacts

## Development Steps

1. Add this plan and run a read-only subagent review.
2. Apply review corrections to the plan.
3. Update TB2 and same-provider docs.
4. Expand the TB2 request template.
5. Update `export-tb2-audit-request.ps1` to generate one or three request files plus a manifest.
6. Update `run-external-audit-flow.ps1` messaging for template-only TB2 mode.
7. Update `normalize-audit-report.ps1` to parse JSON-first and merge multiple reviewer outputs.
8. Run focused smoke checks using temporary projects and sample reviewer results.

## Acceptance Criteria

- TB2 docs no longer imply live relay is available from this skill alone.
- Dry-run TB2 export previews the three-reviewer artifact plan.
- Apply TB2 export writes three reviewer request JSON files and a manifest.
- Single-role TB2 export writes one reviewer request JSON file and records the same manifest fields for that role.
- Each request contains stable IDs, reviewer profile, expected output schema, timeout, provenance policy, and redaction policy.
- Each request defaults to `path-reference` packet transport with `packet_sha256`; embedded packet transport requires explicit opt-in.
- Normalizer can merge three JSON reviewer results into one report.
- Normalizer can merge result wrappers and marks timeout, invalid, or failed reviewers as partial review.
- Normalizer still supports legacy Markdown reviewer output.
- Invalid or partial reviewer output cannot produce an `accept` disposition by default.

## Test Plan

- Run the TB2 exporter in dry-run mode and verify it does not write artifacts.
- Run the TB2 exporter with `-Apply` in a temp project and verify three request files plus manifest exist.
- Parse every generated request with `ConvertFrom-Json`.
- Validate that each request embeds the audit packet, reviewer role, expected schema, and redaction policy.
- Validate that default requests reference the audit packet by path and hash without embedding the full packet body.
- Validate explicit embedded-packet export separately.
- Normalize one JSON result, three JSON results, and a directory of JSON result files.
- Normalize wrapped completed, timeout, invalid, and failed results.
- Normalize legacy Markdown output to confirm fallback behavior remains.
- Test invalid JSON and missing required fields; expected result is failed or partial review, not accept.
- Test invalid enum values, duplicate reviewer IDs, empty result directories, and missing reviewer roles.

## Review Checklist

- Does the plan keep TB2 runtime execution out of this skill?
- Does the request contract give TB2 enough metadata to execute later?
- Does the normalizer have a clear owner and deterministic fallback behavior?
- Does the plan protect against raw prompt/transcript leakage by default?
- Does the plan leave a path for image2dng to complete a three-reviewer audit loop once TB2 runtime tools exist?

