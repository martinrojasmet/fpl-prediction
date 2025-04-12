import prisma from "../prisma/prisma-client.js";

export const getAllFixtures = async () => {
    try {
        const fixtures = await prisma.fixture.findMany();
        return fixtures;
    } catch (error) {
        throw new Error("Error retrieving fixtures: " + error.message);
    }
}

export const getFixtureById = async (id) => {
    try {
        const fixture = await prisma.fixture.findUnique({
            where: { id: parseInt(id, 10) },
        });
        return fixture;
    } catch (error) {
        throw new Error("Error retrieving fixture: " + error.message);
    }
}

export const createFixtures = async (fixturesData) => {
    try {
        const fixtures = await prisma.fixture.createMany({
            data: fixturesData
        });
        return fixtures;
    } catch (error) {
        throw new Error("Error creating fixtures: " + error.message);
    }
}

export const updateFixture = async (id, fixtureData) => {
    try {
        const fixture = await prisma.fixture.update({
            where: { id: parseInt(id, 10) },
            data: fixtureData
        });
        return fixture;
    } catch (error) {
        throw new Error("Error updating fixture: " + error.message);
    }
}

export const deleteFixture = async (id) => {
    try {
        const fixture = await prisma.fixture.delete({
            where: { id: parseInt(id, 10) },
        });
        return fixture;
    } catch (error) {
        throw new Error("Error deleting fixture: " + error.message);
    }
}
