import os
os.system(f"docker rm $(basename $(pwd))")
os.system(f'docker run --name $(basename $(pwd)) --env-file ./.env -p 8081:8081 ssenchyna/$(basename $(pwd)):latest')
