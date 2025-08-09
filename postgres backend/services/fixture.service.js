import prisma from "../prisma/prisma-client.js";

export const getFixtures = async (filters = {}, cursor, limit) => {
    const cursorObj = cursor ? { id: parseInt(cursor, 10) } : undefined;
    const takeLimit = limit ? parseInt(limit, 10) : 50;
    try {
        const fixtures = await prisma.fixture.findMany({
            where: filters,
            take: takeLimit,
            ...(cursorObj && { cursor: cursorObj }),
            skip: cursorObj ? 1 : 0,
            orderBy: { id: 'asc' }
        });
        const nextCursor = fixtures.length === takeLimit ? fixtures[fixtures.length - 1].id : null;
        return {
            data: fixtures,
            nextCursor
        };
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


