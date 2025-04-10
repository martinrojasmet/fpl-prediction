export const fetchAllFixtures = async (req, res) => {
    try {
        res.status(200).json({
            message: "Fixtures retrieved successfully",
        });     
    } catch (error) {
        next(error);
    }
};

export const addFixture = async (req, res) => {
    try {
        res.status(201).json({
            message: "Fixture created successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const modifyFixture = async (req, res) => {
    try {
        res.status(200).json({
            message: "Fixture updated successfully",
        });
    } catch (error) {
        next(error);
    }
};

export const removeFixture = async (req, res) => {
    try {
        res.status(200).json({
            message: "Fixture deleted successfully",
        });
    } catch (error) {
        next(error);
    }
};