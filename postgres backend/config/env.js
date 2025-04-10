import { config } from 'dotenv';

config({ path: '.env' });

export const {
    PORT,
    DATABASE_URL,
    JWT_SECRET,
    JWT_EXPIRATION
} = process.env;