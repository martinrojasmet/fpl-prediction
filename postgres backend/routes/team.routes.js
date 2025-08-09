import { Router } from 'express';
import { fetchTeams, addTeam } from '../controllers/team.controller.js';

const teamRouter = Router();

teamRouter.get("/", fetchTeams);
teamRouter.post("/", addTeam);
// teamRouter.post("/", modifyTeam);

// teamRouter.put("/:id", modifyTeam);
// teamRouter.delete("/:id", removeTeam);

export default teamRouter;