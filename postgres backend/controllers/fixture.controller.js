import { getFixtures, getFixtureById, createFixtures, updateFixture, deleteFixture } from "../services/fixture.service.js";

export const fetchFixtures = async (req, res, next) => {
    try {
        const { cursor, limit, ...filters } = req.query;
        const result = await getFixtures(filters, cursor, limit);
        
        if (!result.data || result.data.length === 0) {
            return res.status(404).json({
                message: "No fixtures found",
            });
        }
        
        res.status(200).json({
            message: "Fixtures retrieved successfully",
            data: result.data,
            nextCursor: result.nextCursor
        });     
    } catch (error) {
        next(error);
    }
};

export const fetchFixture = async (req, res, next) => {
    try {
        const fixtureId = req.params.id;
        const fixture = await getFixtureById(fixtureId);

        if (!fixture || fixture.length === 0) {
            return res.status(404).json({
                message: "Fixture not found"
            });
        }

        res.status(200).json({
            message: "Fixture retrieved successfully",
            data: fixture,
        });
    } catch (error) {
        next(error);
    }
};

export const addFixtures = async (req, res, next) => {
    try {
        const fixturesData = req.body.fixtures;
        const result = await createFixtures(fixturesData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create fixtures",
            });
        }

        res.status(201).json({
            message: "Fixtures created successfully",
            data: result
        });
    } catch (error) {
        next(error);
    }
};

export const modifyFixture = async (req, res, next) => {
    try {
        const fixtureId = req.params.id;
        const fixtureData = req.body.data;
        const result = await updateFixture(fixtureId, fixtureData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to update fixture",
            });
        }

        res.status(200).json({
            message: "Fixture updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removeFixture = async (req, res, next) => {
    try {
        const fixtureId = req.params.id;
        const result = await deleteFixture(fixtureId);

        if (!result) {
            return res.status(400).json({
                message: "Failed to delete fixture",
            });
        }

        res.status(200).json({
            message: "Fixture deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};