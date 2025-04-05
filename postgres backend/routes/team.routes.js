import { Router } from 'express';

const teamRouter = Router();

teamRouter.get("/", (req, res) => { res.send("Get all teams") });
teamRouter.get("/:id", (req, res) => { res.send("Get team by ID") });
teamRouter.post("/", (req, res) => { res.send("Create a new team") });
teamRouter.post("/:id", (req, res) => { res.send("Update a team by ID") });
teamRouter.put("/:id", (req, res) => { res.send("Update a team by ID") });
teamRouter.delete("/:id", (req, res) => { res.send("Delete a team by ID") });

export default teamRouter;