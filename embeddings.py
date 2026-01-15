# 本文件用于下载并获取embedding向量化模型

from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import snapshot_download

# 获取embeddings模型 -- 首次调用时自动下载
def get_embeddings(model_name="BAAI/bge-small-zh-v1.5",device="cpu",**kwargs):
    # 支持更换其他向量化模型
    local_dir = Path("models")/model_name.replace("/", "_")
    if not local_dir.exists():
        print(f'⚠️ 首次使用嵌入模型，正在下载到{local_dir.absolute()}')
        print("💡 提示：需要联网(必需梯子)，完成后可离线使用")
        # 模型下载工具
        snapshot_download(
            repo_id = model_name,
            local_dir = local_dir,
        )
        print('✅ 下载完成！')

    # 构造参数字典
    model_kwargs =  {
            "device":device,
            "local_files_only": True,  # 仅使用本地文件
        }

    # 此处实例化时，把kwargs传入
    _EMBEDDINGS = HuggingFaceEmbeddings(
        model_name = str(local_dir), # 使用本地已下载的模型
        model_kwargs = model_kwargs,
        **kwargs # 允许传入参数
    )
    return _EMBEDDINGS
