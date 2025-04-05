export const getAllGames = async (req, res) => {
    res.send("Get all games");
};

export const getGameById = async (req, res) => {
    res.send("Get game by ID");
};

export const createGame = async (req, res) => {
    res.send("Create a new game");
};

export const updateGame = async (req, res) => {
    res.send("Update a game by ID");
};

export const deleteGame = async (req, res) => {
    res.send("Delete a game by ID");
};