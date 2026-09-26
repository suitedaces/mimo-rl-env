## Polymorphic children are not loaded correctly when hydrating a parent

I'm setting up a polymorphic relation where one parent owns many children of different concrete types — pretty much the canonical example from the README (something like an `Owner` that has many `Pet` records, where `Pet` can be a `Cat` or a `Dog`).

My setup looks roughly like this:

```ts
@Entity()
export class Owner extends BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @PolymorphicChildren(() => Pet, { eager: true })
  pets: Pet[];
}

@Entity()
export class Pet extends BaseEntity implements PolymorphicChildInterface {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @PolymorphicParent(() => Owner)
  owner: Owner;

  @Column()
  entityId: number;

  @Column()
  entityType: string;
}
```

Then in my repository (extending `AbstractPolymorphicRepository<Owner>`) I do something like:

```ts
const owner = await ownerRepo.findOne({ where: { id: 1 } });
// or explicitly: await ownerRepo.hydrateOne(owner);
console.log(owner.pets);
```

In the DB I've manually inserted a few `pet` rows with `entityId = 1` and `entityType = 'Owner'`, so I'm expecting `owner.pets` to contain exactly those rows.

What I get instead is wrong — the `pets` array I end up with on the owner does not match what's actually in the database for that owner. It comes back with the wrong length, and the contents aren't what I'd expect for that parent either. Plays out the same whether I call `find`, `findOne`, or `hydrateOne` directly.

I'd expect the hydrated children array to be exactly the set of child rows belonging to that parent — same count, same entities, no duplicates, nothing missing.

Is the parent → many children case actually working? Happy to share a minimal repro if useful.
