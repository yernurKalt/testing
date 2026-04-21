import { api, setToken, clearToken } from "./api";
import type { AuthToken, User } from "../types";

export async function login(username: string, password: string): Promise<User> {
  const form = new URLSearchParams();
  form.append("username", username);
  form.append("password", password);
  const { data } = await api.post<AuthToken>("/token", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  setToken(data.access_token);
  return await fetchCurrentUser();
}

export async function register(
  username: string,
  email: string,
  password: string
): Promise<User> {
  const { data } = await api.post<User>("/token/register", {
    username,
    email,
    password,
  });
  return data;
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await api.get<User>("/token");
  return data;
}

export function logout() {
  clearToken();
}
