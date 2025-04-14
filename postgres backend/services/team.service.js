import prisma from "../prisma/prisma-client.js";
import { parseValueByType } from "../utils/validation.utils.js";

export const getAllTeams = async (queries) => {
    try {
        const validFields = prisma.team.fields;
        const errors = [];
        const where = {};

        for (const [key, value] of Object.entries(queries)) {
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

        const teams = await prisma.team.findMany({ where });
        return teams;
    } catch (error) {
        throw new Error(`Error retrieving teams: ${error.message}`);
    }
};

export const createTeam = async (teamData) => {
    try {
        const team = await prisma.team.create({
            data: teamData,
        });
        return team;
    } catch (error) {
        throw new Error("Error creating team: " + error.message);
    }
}
