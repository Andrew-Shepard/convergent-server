#!/command/execlineb -P
# https://danyspin97.org/blog/getting-started-with-execline-scripting/
with-contenv
foreground { bash /app/utility/db_init.sh }
s6-setuidgid convergent python /app/convergent
