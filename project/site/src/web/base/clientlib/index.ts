export * from "./models"
export * from "django-client-framework"
import { LoginAPI, LogoutAPI } from "./auth"

export const Login = new LoginAPI()
export const Logout = new LogoutAPI()
