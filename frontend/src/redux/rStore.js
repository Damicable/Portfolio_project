import { createStore, applyMiddleware } from 'redux';
import {thunk} from 'redux-thunk';
import recipeReducer from './recipeReducer';

const store = createStore(recipeReducer, applyMiddleware(thunk));

export default store;