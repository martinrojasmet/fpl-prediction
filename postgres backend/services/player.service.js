import prisma from "../prisma/prisma-client";

export const getAllPlayers = async () => {
    try {
        const players = await prisma.player.findMany();
        return players;
    } catch (error) {
        throw new Error("Error retrieving players: " + error.message);
    }
}