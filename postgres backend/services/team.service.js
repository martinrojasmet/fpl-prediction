import prisma from "../prisma/prisma-client.js";
import { parseValueByType } from "../utils/validation.utils.js";

export const getTeams = async (filters = {}, cursor, limit) => {
    try {
        const validFields = prisma.team.fields;
        const errors = [];
        const where = {};
        const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
        const takeLimit = limit ? parseInt(limit, 10) : 50;

        for (const [key, value] of Object.entries(filters)) {
            if (!(key in validFields)) {
                errors.push(`Invalid field: '${key}'`);
                continue;
            }
            const fieldType = validFields[key].typeName;
            try {
                where[key] = parseValueByType(fieldType, value, key);
            } catch (error) {
                errors.push(error.message);
            }
        }

        if (errors.length > 0) {
            throw new Error(`Validation errors: ${errors.join('; ')}`);
        }

        const teams = await prisma.team.findMany({
            where,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });

        const nextCursor = teams.length === takeLimit ? teams[teams.length - 1].id : null;
        return {
            data: teams,
            nextCursor
        };
    } catch (error) {
        throw new Error(`Error retrieving teams: ${error.message}`);
    }
};

export const createTeams = async (teamsData) => {
    try {
        const teams = await prisma.team.createMany({
            data: teamsData,
        });
        return teams;
    } catch (error) {
        throw new Error("Error creating teams: " + error.message);
    }
}

