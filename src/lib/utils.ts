import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Strips currency symbols and normalizes price strings
 * @param price - Price string with any currency symbol (£, Rs, $, etc.)
 * @returns number - Cleaned numeric value
 */
export function stripCurrency(price: string | number): number {
  if (typeof price === 'number') return price;
  
  // Remove currency symbols, commas, and whitespace
  const cleaned = price.replace(/[£$€₹Rs.,\s]/g, '');
  return parseFloat(cleaned) || 0;
}

/**
 * Formats a number or price string without currency symbol
 * @param amount - Number or price string to format
 * @returns string - Formatted number with commas
 */
export function formatPrice(amount: number | string): string {
  const num = typeof amount === 'string' ? stripCurrency(amount) : amount;
  return num.toLocaleString('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  });
}
