import { Router } from "express";
import { fetchFixtures, fetchFixture, addFixtures, modifyFixture, removeFixture } from "../controllers/fixture.controller.js";

const fixtureRouter = Router();

fixtureRouter.get("/", fetchFixtures);
fixtureRouter.get("/:id", fetchFixture);
fixtureRouter.post("/", addFixtures);
fixtureRouter.put("/:id", modifyFixture);
fixtureRouter.delete("/:id", removeFixture);

export default fixtureRouter;