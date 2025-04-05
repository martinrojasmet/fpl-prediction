import { Router } from 'express';
import { getAllTeams, getTeamById, createTeam, updateTeam, deleteTeam } from '../controllers/team.controller.js';

const teamRouter = Router();

teamRouter.get("/", getAllTeams);
teamRouter.get("/:id", getTeamById);
teamRouter.post("/", createTeam);
teamRouter.post("/:id", updateTeam);
teamRouter.put("/:id", updateTeam);
teamRouter.delete("/:id", deleteTeam);

export default teamRouter;