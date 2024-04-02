
             %
             %%
             %%#
             %-+%
           %%%+.#
         #%#%.*=-%#
       #%=.%+-*%-:%%
      %%#*.*.#--%--*=%
     #%*%*.*.+- +-:%*%#     ███╗   ██╗ █████╗ ██████╗ ████████╗██╗  ██╗ █████╗ 
    #@:= *.%::#+:%%.=.%#    ████╗  ██║██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██╔══██╗
     %%:*#.#*:*%=:*:=%%     ██╔██╗ ██║███████║██████╔╝   ██║   ███████║███████║
      %*-*:..=-%*:*:##      ██║╚██╗██║██╔══██║██╔═══╝    ██║   ██╔══██║██╔══██║
       ##+*--+-%=#+##       ██║ ╚████║██║  ██║██║        ██║   ██║  ██║██║  ██║
        #%#+=+=%*%%#        ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
          #%#%#%%#                    Decentralized Compute for Multi-Agent Ops   
                                                                  www.naptha.ai

# Naptha Python SDK

## Install

```
pip install naptha-sdk
```

## Get Started

### Create an Account

Create an account on the [Hub](https://hub.naptha.ai/) and buy a Naptha subscription ($1 for 1000 credits).

```
naptha credits
```

### Explore Coworkers on the Network

Navigate to the Coworkers page. Coworkers are users that run full compute nodes on the network, and engage in cooperations (Coops) for a set fee. 

Alternatively, you can use the CLI to see a list of available Coworkers:

```
naptha coworkers
```

And their pricing plans:

```
naptha plans
```

Make note of a Node ID for running a Co-Op below.

### Check out available Co-Ops

Navigate to the Co-Ops page. You can think of a Co-Op like a decentralized workflow or app that you can take part in with one or more Coworkers. Rather than running on a central server, Co-Ops can run across many compute nodes with many local data sources, opening up new use cases. Co-Ops typically involve one or more LLMs, along with humans in the loop. Coworkers can set a price for running Co-Ops. 

You can also use the CLI to explore available Co-Ops that you can take part in with Coworkers, along with their price:

```
naptha coops
```

### Create your own Co-Op

(Coming Soon)

### Run a Co-Op

Once you've found a Coworker and a Co-Op you'd like to engage in, you can run and view the results using the Hub. 

Alternatively, you can use the commandline tool to connect with the Coworker and run the Co-Op (replace the node ID with a real node ID found on the Hub).

```
# usage: naptha run <coworker_id> <coop_id> <coop args>
naptha run node:58d8iv526jr6fbxlndrw chat_coop --prompt "what is the capital of france?"
```

## Check how much you spent

```
naptha purchases
```

# Run a Node

You can run your own Naptha Coworker node to become a Coworker, and earn rewards for engaging in Co-Ops. Follow the instructions at https://github.com/NapthaAI/coworker-node