import { getGameById, createGames } from "../services/game.service.js";

export const fetchAllGames = async (req, res) => {
    try {
        res.status(200).json({
            message: "Games retrieved successfully",
        });
    }
    catch (error) {
        next(error);
    }
};

export const fetchGameById = async (req, res, next) => {
    try {
        const result = await getGameById(req.params.id);

        if (!result || result.length === 0) {
            return res.status(404).json({
                message: "Game not found",
            });
        }

        res.status(200).json({
            message: "Game retrieved successfully",
            data: result
        });
    }
    catch (error) {
        next(error);
    }
};

export const addGames = async (req, res, next) => {
    
    try {
        const gamesData = req.body.games;
        const result = await createGames(gamesData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create game",
            });
        }

        res.status(201).json({
            message: "Game created successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const modifyGame = async (req, res) => {
    try {
        res.status(200).json({
            message: "Game updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removeGame = async (req, res) => {
    try {
        res.status(200).json({
            message: "Game deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};