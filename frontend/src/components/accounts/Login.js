import { LockClosedIcon } from "@heroicons/react/solid";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../redux/actions/auth";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const token = useSelector((state) => state.auth.token);

  const dispatch = useDispatch();

  console.log(token)

  useEffect(() => {
    if (token) {
      console.log(token)
      navigate("/dashboard");
    }
  }, [token, navigate]);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    dispatch(
      login({
        username: username,
        password: password,
      })
    );
  };

  return (
    <>
      <div className="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h2 className="mt-6 text-3xl font-light text-[#A51E1E]">
              Login to your account
            </h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleFormSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Username
                </label>
                <input
                  id="username"
                  name="username"
                  type="username"
                  autoComplete="username"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-[#D42B2B] focus:border-[#D42B2B] focus:z-10 sm:text-sm"
                  placeholder="Username"
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-[#D42B2B] focus:border-[#D42B2B] focus:z-10 sm:text-sm"
                  placeholder="Password"
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-[#D42B2B] hover:bg-[#A51E1E] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#D42B2B]"
              >
                <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                  <LockClosedIcon
                    className="h-5 w-5 text-[#A51E1E] group-hover:text-[#931919]"
                    aria-hidden="true"
                  />
                </span>
                Login
              </button>
            </div>
            <div className="text-sm">
              <Link
                to="/register"
                className="font-medium text-[#D42B2B] hover:text-[#A51E1E]"
              >
                Don't have an account? Register
              </Link>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
