import { Router } from 'express';
import { fetchAllTeams, addTeam, modifyTeam, removeTeam } from '../controllers/team.controller.js';

const teamRouter = Router();

teamRouter.get("/", fetchAllTeams);
teamRouter.post("/", addTeam);
teamRouter.put("/:id", modifyTeam);
teamRouter.delete("/:id", removeTeam);

export default teamRouter;