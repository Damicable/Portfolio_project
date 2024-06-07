import {
  ADD_CATEGORY,
  ADD_COOKTIME,
  ADD_INGREDIENTS,
  ADD_PICTURE,
  ADD_PROCEDURES,
} from "./types";

export const addIngredients = (ingredients) => {
  console.log("forms", ingredients)
  return {
    type: ADD_INGREDIENTS,
    payload: ingredients,
  };
};

export const addProcedures = (procedures) => {
  console.log("forms", procedures)
  return {
    type: ADD_PROCEDURES,
    payload: procedures,
  };
};

export const addCooktime = (cook_time) => {
  console.log("forms", cook_time)
  return {
    type: ADD_COOKTIME,
    payload: cook_time,
  };
};

export const addCategory = (category) => {
  console.log("forms", category)
  return {
    type: ADD_CATEGORY,
    payload: category,
  };
};

export const addPicture = (picture) => {
  console.log("forms", picture)
  return {
    type: ADD_PICTURE,
    payload: picture,
  };
};
