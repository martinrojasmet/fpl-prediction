import { getPlayers, getPlayersFPLNames, getPlayersUnderstatNames, createPlayers, updatePlayersUnderstatNames, deletePlayerByFPLName } from "../services/player.service.js";

export const fetchPlayers = async (req, res, next) => {
    try {
        const { cursor, limit, ...filters } = req.query;
        const result = await getPlayers(filters, cursor, limit);
        
        if (!result.data || result.data.length === 0) {
            return res.status(404).json({
                message: "No players found",
            });
        }
        
        res.status(200).json({
            message: "Players retrieved successfully",
            data: result.data,
            nextCursor: result.nextCursor
        });
    } catch (error) {
        next(error);
    }
};

export const fetchAllPlayersFPLNames = async (req, res, next) => {
    try {
        const result = await getPlayersFPLNames();

        if (!result || result.length === 0) {
            return res.status(404).json({
                message: "No players found",
            });
        }

        res.status(200).json({
            message: "Players FPL names retrieved successfully",
            data: result
        });
    } catch (error) {
        next(error);
    }
};

export const fetchAllPlayersUnderstatNames = async (req, res, next) => {
    try {
        const result = await getPlayersUnderstatNames();

        if (!result || result.length === 0) {
            return res.status(404).json({
                message: "No players found",
            });
        }

        res.status(200).json({
            message: "Players Understat names retrieved successfully",
            data: result
        });
    } catch (error) {
        next(error);
    }
};

export const addPlayers = async (req, res, next) => {
    try {
        const playersData = req.body.players;
        console.log("Adding players:", playersData);
        const result = await createPlayers(playersData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create players",
            });
        }

        res.status(201).json({
            message: "Players created successfully",
            data: result
        });
    } catch (error) {
        console.error("Error adding players:", error);
        next(error);
    }
}

export const modifyPlayer = async (req, res, next) => {
    try {
        res.status(200).json({
            message: "Player updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removePlayer = async (req, res, next) => {
    try {
        res.status(200).json({
            message: "Player deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const modifyPlayersUnderstatNames = async (req, res, next) => {
    try {
        const result = await updatePlayersUnderstatNames(req.body);

        if (!result) {
            return res.status(400).json({
                message: "Failed to update players",
            });
        }

        res.status(200).json({
            message: "Players updated successfully",
            data: result
        });
    } catch (error) {
        next(error);
    }
}

export const removePlayerByFPLName = async (req, res, next) => {
    try {
        const fplName = req.params.fpl_name;
        const result = await deletePlayerByFPLName(fplName);

        if (!result) {
            return res.status(404).json({
                message: "Player not found",
            });
        }

        res.status(200).json({
            message: "Players deleted successfully",
        });
    } catch (error) {
        next(error);
    }
}