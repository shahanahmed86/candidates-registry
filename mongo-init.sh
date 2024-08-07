mongo -- "$MONGO_INITDB_DATABASE" <<EOF
  db.createUser({
    user: "$MONGO_USERNAME",
    pwd: "$MONGO_PASSWORD",
    roles: [
      { role: "readWrite", db: "$MONGO_INITDB_DATABASE" }
    ]
  })
EOF

DIR="/dump"
if [ -d "$DIR" ]; then
  echo "restoring the dump from '${DIR}' ..."
  mongorestore -d "$MONGO_INITDB_DATABASE" -u "$MONGO_USERNAME" -p "$MONGO_PASSWORD" /dump
else
  echo "'${DIR}' not found. Can not restore."
fi