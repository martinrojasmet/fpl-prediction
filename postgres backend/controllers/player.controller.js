export const fetchAllPlayers = async (req, res) => {
    try {
        res.status(200).json({
            message: "Players retrieved successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const addPlayer = async (req, res) => {
    try {
        res.status(201).json({
            message: "Player created successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const modifyPlayer = async (req, res) => {
    try {
        res.status(200).json({
            message: "Player updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removePlayer = async (req, res) => {
    try {
        res.status(200).json({
            message: "Player deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};