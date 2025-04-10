import prisma from "../prisma/prisma-client";

export const getAllFixtures = async () => {
    try {
        const fixtures = await prisma.fixture.findMany();
        return fixtures;
    } catch (error) {
        throw new Error("Error retrieving fixtures: " + error.message);
    }
}
