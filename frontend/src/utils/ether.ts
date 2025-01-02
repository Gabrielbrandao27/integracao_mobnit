import { toUtf8String } from "ethers";

export const hex2str = (hex: string): string => {
  try {
    return toUtf8String(hex);
  } catch {
    // cannot decode hex payload as a UTF-8 string
    return hex;
  }
};
