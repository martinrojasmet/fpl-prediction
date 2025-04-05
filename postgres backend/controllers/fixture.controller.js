export const getAllFixtures = async (req, res) => {
    res.send("Get all fixtures");
};

export const getFixtureById = async (req, res) => {
    res.send("Get fixture by ID");
};

export const createFixture = async (req, res) => {
    res.send("Create a new fixture");
};

export const updateFixture = async (req, res) => {
    res.send("Update a fixture by ID");
};

export const deleteFixture = async (req, res) => {
    res.send("Delete a fixture by ID");
};