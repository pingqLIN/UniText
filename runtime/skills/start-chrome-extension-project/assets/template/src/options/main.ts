import { readPreference, writePreference } from "../shared/storage";

const input = document.querySelector<HTMLInputElement>("#preference");
const save = document.querySelector<HTMLButtonElement>("#save");
const status = document.querySelector<HTMLDivElement>("#status");

const hydrate = async () => {
  const preference = await readPreference();

  if (input) {
    input.value = preference ?? "";
  }

  if (status) {
    status.textContent = "Settings loaded.";
  }
};

save?.addEventListener("click", async () => {
  if (!input || !status) {
    return;
  }

  await writePreference(input.value.trim());
  status.textContent = "Saved.";
});

void hydrate();
