export const getAllTeams = async (req, res) => {
    res.send("Get all teams");
};

export const getTeamById = async (req, res) => {
    res.send("Get team by ID");
};

export const createTeam = async (req, res) => {
    res.send("Create a new team");
};  

export const updateTeam = async (req, res) => {
    res.send("Update a team by ID");
};

export const deleteTeam = async (req, res) => {
    res.send("Delete a team by ID");
};