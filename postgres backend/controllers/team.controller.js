import { getAllTeams, createTeams } from "../services/team.service.js";

export const fetchAllTeams = async (req, res, next) => {
    try {
        const teams = await getAllTeams(req.query);

        if (!teams || teams.length === 0) {
            return res.status(404).json({
                message: "No teams found",
            });
        }
        
        res.status(200).json({
            message: "Teams retrieved successfully",
            data: teams
        });
    } catch (error) {
        next(error);
    }
};

export const addTeam = async (req, res, next) => {
    try {
        const teamsData = req.body.teams;
        const result = await createTeams(teamsData);

        if (!result) {
            return res.status(400).json({
                message: "Failed to create team",
            });
        }

        res.status(201).json({
            message: "Team created successfully",
        });
    } catch (error) {
        next(error);
    }
};