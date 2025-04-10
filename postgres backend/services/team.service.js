import prisma from "../prisma/prisma-client";

export const getAllTeams = async () => {
    try {
        const teams = await prisma.team.findMany();
        return teams;
    } catch (error) {
        throw new Error("Error retrieving teams: " + error.message);
    }
}