// actions.js
import axios from 'axios';
import {
  FETCH_RECIPES_REQUEST,
  FETCH_RECIPES_SUCCESS,
  FETCH_RECIPES_FAILURE
} from './recipeActionTypes';

const fetchRecipesRequest = () => ({
  type: FETCH_RECIPES_REQUEST,
});

const fetchRecipesSuccess = recipes => ({
  type: FETCH_RECIPES_SUCCESS,
  payload: recipes,
});

const fetchRecipesFailure = error => ({
  type: FETCH_RECIPES_FAILURE,
  payload: error,
});

export const fetchRecipes = () => {
  return dispatch => {
    dispatch(fetchRecipesRequest());
    axios.get('http://localhost:5000/api/recipes/all')
      .then(response => {
        const recipes = response.data;
        dispatch(fetchRecipesSuccess(recipes));
      })
      .catch(error => {
        dispatch(fetchRecipesFailure(error.message));
      });
  };
};
