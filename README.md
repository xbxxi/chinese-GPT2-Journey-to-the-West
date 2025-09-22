Training GPT2 Chinese from zero 

1.Description:

从头训练一个82M的中文GPT2模型，采用西游记小说的部分章节作为训练集。训练15个周期，batchsize=8。最终可以续写10句以上的西游记小说。

2.Start:

(1)environment

首先，我们需要下载相关的环境。

pip install -r requirements.txt

(2)dataset

准备中文语料，放置在./data/文件夹下，将语料由.txt文件更改为input.json文件，可以使用以下命令生成：
python txt_to_json.py

按照参考样例./train.json更改input.json文件格式,由于数据集内容为原始的小说内容，包含着大量的非法字符和json读取不支持的控制字符，因此我们对原始数据集文件进行处理，去除其中非法字符，生成预处理好的数据集文件train.json。

python clr_ctrl.py

(3)Model

在model_config 定义初始GPT-2模型的超参数配置，

"initializer_range": 0.02 ： 定义了模型参数（如权重矩阵）在初始化时的标准差，权重会在均值为0，标准差为0.02的正态分布中进行随机初始化。

"layer_norm_epsilon": 1e-05 ： 用于层归一化的常数，用于避免在归一化过程中出现除以零的情况。设置值为1e-05，用于稳定训练。

"n_ctx": 1024 ： 表示模型上下文窗口的大小，GPT-2 在生成文本时会考虑的最大序列长度。最大长度设为1024，即模型一次最多能处理1024个 token。

"n_embd": 768 ： 表示每个token的嵌入维度大小，即模型中词向量的维度。设置为768，即每个词汇的表示向量是768维的。

"n_head": 12 ： 表示自注意力机制中的注意力头的数量。设置为12，即模型的多头注意力机制中有12个独立的头。

"n_layer": 10 ： 表示 Transformer 编码器中的层数。在这里，设置为 12，即模型有 12 层堆叠的 Transformer 块。

"n_positions": 1024 ： 表示模型可以处理的最大位置索引，即序列中的最大位置数。最大位置数为 1024，和 n_ctx一致，表示模型最多能处理1024个位置的token。

"vocab_size": 13317 ： 表示词汇表的大小，即模型可以识别和生成的词汇数量。在这里，词汇表大小为 21128，表示该模型可以处理的词汇量为21128个不同的 token。

(4)Training

现在，我们可以使用我们处理好的数据集来训练我们的初始gpt2模型，使用如下命令：

python train.py   --model_config config/model_config_small.json   --tokenized_data_path data/tokenized/   --tokenizer_path cache/vocab_small.txt   --raw_data_path data/train.json   --epochs 15   --log_step 200   --stride 512   --output_dir model/   --device 0,1   --num_pieces 100   --raw

在这个过程中，我们可以看到命令窗口打印出模型的config文件，定义了模型的结构；同时也打印出了模型的参数量

Print Model config config: { "attn_pdrop": 0.1, "embd_pdrop": 0.1, "finetuning_task": null, "initializer_range": 0.02, "layer_norm_epsilon": 1e-05, "n_ctx": 1024, "n_embd": 768, "n_head": 12, "n_layer": 10, "n_positions": 1024, "num_labels": 1, "output_attentions": false, "output_hidden_states": false, "output_past": true, "pruned_heads": {}, "resid_pdrop": 0.1, "summary_activation": null, "summary_first_dropout": 0.1, "summary_proj_to_labels": true, "summary_type": "cls_index", "summary_use_proj": true, "torchscript": false, "use_bfloat16": false, "vocab_size": 13317 } number of parameters: 81894144

训练过程中，每个epoch对应的模型都将存储在./model/目录下，最终训练好的模型将存储在./model/final_model/路径中。

(5)Generate

现在，我们可以使用我们用目标语料训练生成的模型来进行文字生成，使用如下命令：

python generate.py   --device 1   --length 1000   --tokenizer_path cache/vocab_small.txt   --model_path model/final_model   --prefix "[CLS]萧炎大喝一声"   --topp 1   --temperature 1.0 --save_samples --save_samples_path ./mnt/

3.Result

最终会生成1个文字样本，存储在./mnt/目录下，如下所示：

======================================== SAMPLE 1 ========================================

孙悟空大喝一声：师傅！若不可，不知是我等他的？”行者道：“师父，他就把他是这个，你不能得有何处，我这等我不曾与你这般儿的和你怎么这里，他就是他怎么？”行者道：“师父啊，你不知是他的？”行者道：“你们也是我，你怎么？”行者道：“你不要吃他也不知他的人，你这些甚么？”那里，我与你怎么，我们，只是个个妖精。”行者道：“我说得他，却又不知他一个甚么？”行者道：“他，就是个甚么？”那怪道：“我也是这个大王大圣道：“我等我的。”行者道：“这般不是。”行者笑道：“他，只是甚么？”行者道：“是甚么？”三藏道：“老孙的？”老孙行者道：“我等我是我也。”老孙行者道：“我的？”行者闻言，却不知他的人。”行者道：“你们的一声。”行者笑道：“我也是我也有几年前道：“那里去，这猴儿，你这等我的？”八戒道：“是我师父是这里人家，我不是个人家？”老孙
行者道：“你是我去也罢。”行囊，我师道：“你不要不是老孙，我们，我也不要你这和你怎么？”行者道

================================================================================

