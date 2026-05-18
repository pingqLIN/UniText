const preferenceKey = "starterPreference";

export const readPreference = async (): Promise<string | undefined> => {
  const result = await chrome.storage.sync.get(preferenceKey);
  const value = result[preferenceKey];

  if (typeof value !== "string" || value.length === 0) {
    return;
  }

  return value;
};

export const writePreference = async (value: string): Promise<void> => {
  await chrome.storage.sync.set({ [preferenceKey]: value });
};
