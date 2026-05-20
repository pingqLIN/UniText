export const messageType = {
  ping: "PING"
} as const;

export type MessageType = (typeof messageType)[keyof typeof messageType];
