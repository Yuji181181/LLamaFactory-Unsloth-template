# GitHubへのプッシュ手順

このドキュメントでは、このテンプレートリポジトリをGitHubにプッシュする手順を説明します。

## 📋 前提条件

- GitHubアカウントを持っている
- Gitがインストールされている
- SSHキーまたはPersonal Access Tokenが設定されている

## 🚀 プッシュ手順

### ステップ1: Gitリポジトリを初期化

```bash
# 現在のディレクトリで実行
git init
```

### ステップ2: すべてのファイルを追加

```bash
git add .
```

### ステップ3: 初回コミット

```bash
git commit -m "Initial commit: LLaMA-Factory + Unsloth Competition Template

- Complete setup scripts for environment configuration
- Unsloth integration for 2x faster training
- Support for SFT, DPO, and SimPO
- Comprehensive documentation in Japanese
- Synthetic data generation workflow
- Ready-to-use configuration templates"
```

### ステップ4: GitHubでリポジトリを作成

1. ブラウザで https://github.com/new にアクセス
2. 以下の情報を入力：
   - **Repository name**: `LLamaFactory-Unsloth-template`（または任意の名前）
   - **Description**: `LLM Competition Template with LLaMA-Factory + Unsloth | 2x faster fine-tuning`
   - **Public** または **Private** を選択
   - **Initialize this repository with:** すべてチェックを外す（重要！）
3. **Create repository** をクリック

### ステップ5: リモートリポジトリを追加

```bash
# HTTPSの場合
git remote add origin https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template.git

# SSHの場合（推奨）
git remote add origin git@github.com:YOUR_USERNAME/LLamaFactory-Unsloth-template.git
```

**注意**: `YOUR_USERNAME` を自分のGitHubユーザー名に置き換えてください。

### ステップ6: メインブランチにプッシュ

```bash
git branch -M main
git push -u origin main
```

## ✅ プッシュ完了後の確認

ブラウザで以下を確認してください：
- https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template

以下が表示されていればOKです：
- ✅ README.mdが表示されている
- ✅ docs/ ディレクトリが存在する
- ✅ configs/ ディレクトリが存在する
- ✅ setup.sh が実行可能になっている

## 🎯 テンプレートリポジトリとして設定（推奨）

他のユーザーがこのリポジトリをテンプレートとして使用できるようにします。

### 手順

1. リポジトリページで **Settings** をクリック
2. **General** セクションで **Template repository** にチェック
3. 保存

これで、他のユーザーが **Use this template** ボタンでこのリポジトリをベースに新しいプロジェクトを作成できます！

## 📝 リポジトリ設定の推奨事項

### Description（説明）

```
LLM Competition Template with LLaMA-Factory + Unsloth | 2x faster fine-tuning with SFT, DPO, SimPO support
```

### Topics（タグ）

以下のトピックを追加することを推奨します：

```
llm
fine-tuning
llama-factory
unsloth
template
competition
machine-learning
pytorch
cuda
deep-learning
nlp
transformers
```

### About（リポジトリ情報）

- **Website**: （あれば）プロジェクトのウェブサイトURL
- **Topics**: 上記のトピックを追加

## 🔒 .gitignoreの確認

以下のファイル/ディレクトリが除外されていることを確認してください：

```bash
# 確認コマンド
git status

# 以下が表示されないことを確認
# - LLaMA-Factory/
# - .venv/
# - outputs/
# - *.log
```

もし表示される場合は、`.gitignore` が正しく設定されているか確認してください。

## 📊 リポジトリの統計

プッシュ後、以下を確認できます：

```bash
# ファイル数
find . -type f ! -path "./.git/*" | wc -l

# コミット数
git log --oneline | wc -l

# ブランチ
git branch -a
```

## 🔄 更新をプッシュする場合

テンプレートを更新した場合：

```bash
# 変更を確認
git status

# 変更を追加
git add .

# コミット
git commit -m "Update: 変更内容の説明"

# プッシュ
git push
```

## 🌟 README Badgesの追加（オプション）

README.mdに以下のバッジを追加できます：

```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/LLamaFactory-Unsloth-template?style=social)](https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/LLamaFactory-Unsloth-template?style=social)](https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template/network/members)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/LLamaFactory-Unsloth-template)](https://github.com/YOUR_USERNAME/LLamaFactory-Unsloth-template/issues)
```

## 📚 参考リンク

- [GitHub Docs - Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub Docs - Template repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- [Git Documentation](https://git-scm.com/doc)

---

**プッシュが完了したら、リポジトリのURLを共有してください！** 🎉
