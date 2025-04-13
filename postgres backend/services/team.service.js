import prisma from "../prisma/prisma-client.js";

export const getAllTeams = async (params) => {
    try {
        // Todo: add validation for numbers
        const where = Object.fromEntries(
            Object.entries(params).filter(([key]) => Object.keys(prisma.team.fields).includes(key))
        );

        const teams = await prisma.team.findMany({
            where: where
        });
        return teams;
    } catch (error) {
        throw new Error("Error retrieving teams: " + error.message);
    }
}

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
