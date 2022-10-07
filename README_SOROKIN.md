 python3 experiments/validator.py --config-path=configs --config-name=validator.yaml
 python3 experiments/dqn_trainer.py --config-path=configs --config-name=retro.yaml 
 python3 experiments/gen_instances.py --config-path=configs --config-name=retro.yaml

 docker run -dit --gpus all --name sorokin_new  --volume ~/dev/retro_branching:/retro_branching 8a21113782ad
 docker exec -it 8b9c53ffe36f /bin/bash
