/**
 * Logger utility - disables console logs in production
 */

const IS_DEV = import.meta.env.DEV

export const logger = {
  log: (...args) => {
    if (IS_DEV) console.log(...args)
  },
  error: (...args) => {
    if (IS_DEV) console.error(...args)
  },
  warn: (...args) => {
    if (IS_DEV) console.warn(...args)
  }
}
