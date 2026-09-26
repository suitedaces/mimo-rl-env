Incorrect schema generation in the beta release
> well it doesn't really work since it generate 2 primary keys :/
> ```ts
> export const account = pgTable("account", {
>   id: serial("id").primaryKey(),
>   accountId: text("account_id").notNull(),
>   providerId: text("provider_id").notNull(),
>   userId: serial("user_id")
>     .primaryKey() // <-- this is wrong!
>     .notNull()
>     .references(() => user.id, { onDelete: "cascade" }),
>   accessToken: text("access_token"),
>   refreshToken: text("refresh_token"),
>   idToken: text("id_token"),
>   accessTokenExpiresAt: timestamp("access_token_expires_at"),
>   refreshTokenExpiresAt: timestamp("refresh_token_expires_at"),
>   scope: text("scope"),
>   password: text("password"),
>   createdAt: timestamp("created_at").notNull(),
>   updatedAt: timestamp("updated_at").notNull(),
> });
> ``` 

 _Originally posted by @body20002 in [#3308](https://github.com/better-auth/better-auth/issues/3308#issuecomment-3049875914)_
