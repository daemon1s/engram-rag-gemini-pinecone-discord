"use server"

import { signIn } from "@/auth"

export async function loginWithDiscord() {
  await signIn("discord", { redirectTo: "/dashboard" })
}
