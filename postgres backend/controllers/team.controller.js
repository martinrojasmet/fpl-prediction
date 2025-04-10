export const fetchAllTeams = async (req, res) => {
    try {
        res.status(200).json({
            message: "Teams retrieved successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const addTeam = async (req, res) => {
    try {
        res.status(201).json({
            message: "Team created successfully",
        });
    } catch (error) {
        next(error);
    }
};  

export const modifyTeam = async (req, res) => {
    try {
        res.status(200).json({
            message: "Team updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removeTeam = async (req, res) => {
    try {
        res.status(200).json({
            message: "Team deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};