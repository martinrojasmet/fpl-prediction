export const getAllPlayers = async (req, res) => {
    res.send("Get all players");
};

export const getPlayerById = async (req, res) => {
    res.send("Get player by ID");
}

export const createPlayer = async (req, res) => {
    res.send("Create a new player");
};

export const updatePlayer = async (req, res) => {
    res.send("Update a player by ID");
}

export const deletePlayer = async (req, res) => {
    res.send("Delete a player by ID");
};