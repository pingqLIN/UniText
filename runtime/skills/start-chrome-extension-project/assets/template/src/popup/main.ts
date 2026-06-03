import { readPreference, writePreference } from "../shared/storage";

const status = document.querySelector<HTMLDivElement>("#status");
const save = document.querySelector<HTMLButtonElement>("#save");

const render = async () => {
  if (!status) {
    return;
  }

  const preference = await readPreference();
  status.textContent = preference
    ? `Saved preference: ${preference}`
    : "No preference saved yet.";
};

save?.addEventListener("click", async () => {
  await writePreference("starter-ready");
  await render();
});

void render();
