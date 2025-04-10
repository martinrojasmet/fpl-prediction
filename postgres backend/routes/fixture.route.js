import { Router } from "express";
import { fetchAllFixtures, addFixture, modifyFixture, removeFixture } from "../controllers/fixture.controller.js";

const fixtureRouter = Router();

fixtureRouter.get("/", fetchAllFixtures);
fixtureRouter.post("/", addFixture);
fixtureRouter.put("/:id", modifyFixture);
fixtureRouter.delete("/:id", removeFixture);

export default fixtureRouter;