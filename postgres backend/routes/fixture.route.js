import { Router } from "express";
import { fetchAllFixtures, fetchFixture, addFixtures, modifyFixture, removeFixture } from "../controllers/fixture.controller.js";

const fixtureRouter = Router();

fixtureRouter.get("/", fetchAllFixtures);
fixtureRouter.get("/:id", fetchFixture);
fixtureRouter.post("/", addFixtures);
fixtureRouter.put("/:id", modifyFixture);
fixtureRouter.delete("/:id", removeFixture);

export default fixtureRouter;