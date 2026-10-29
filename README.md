# Revision app

> [!NOTE]
> This app in its current state is extremely vibecoded.
>
> The code quality is not guaranteed to be amazing.

This app uses plain HTML and browser JavaScript. No Node.js, packages, or build
step are needed.

## Question and Answer Sets

By default, the application comes with several JSON Question and answer sets, that can be found [here](./qa-sets/).

These sets are for the following subjects:
- COSC3045 Essentials of Computing (2650)
- COSC1114 Operating Systems PRinciples (2650)

## Loading content

You can load a question set in two ways: automatic load or manual load.

### Automatic load (HTTP server)

Start the local server:

```
uv run serve.py
```

Or use `python serve.py`. Then open the address that the server prints.

The app loads `eoc-revision.json` from the same folder as `index.html`. To load
another file, add the `data` query parameter:

```
http://localhost:8000/?data=qa-sets/eoc-revision.json
```

The value can be a relative path or an absolute URL. The server does not reload
the page when you change files. Reload the browser instead.

### Manual load (file picker)

1. Open `index.html` in the browser.
2. Click **Load JSON**.
3. Select a JSON file.

Use this method when you open the file directly (`file://`). Browsers block the
automatic load on `file://`.

### Checks and stored progress

The app checks the JSON before it shows the data. If the JSON is not correct,
the app shows the error and keeps the current data.

The browser stores your progress for each data source. To clear the progress,
open **Progress** and click **Reset progress on this device**.

## JSON format

The file contains one JSON object with these keys:

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `title` | string | No | Page title. Default: `Revision`. |
| `setLabel` | string | No | Text before each set name. Default: `Tute `. |
| `drills` | boolean | No | Show the calculation drills. Default: `true`. |
| `sets` | array of strings | Yes | Set names. Each name must be unique and must have at least one question. |
| `groups` | object | No | Maps a group name to an array of set names. |
| `questions` | array of objects | Yes | The questions. See below. |
| `videos` | object | Yes | Maps a video key to `[YouTube ID, title, channel, duration]`. Use `{}` if there are no videos. |
| `questionVideos` | object | Yes | Maps a question `id` to an array of video keys. Use `{}` if there are no videos. |
| `images` | object | No | Maps an image key to a base64 `data:image/...` URI. |

### Question fields

| Key | Type | Required | Meaning |
| --- | --- | --- | --- |
| `id` | string | Yes | Unique ID. Do not start the ID with `calc_`. |
| `set` | string | Yes | Set name. Must occur in `sets`. |
| `n` | integer | Yes | Question number in the set. Must be positive. |
| `q` | string | Yes | Question text. |
| `src` | string | Yes | Source text. See "Source text" below. |
| `type` | string | No | `open`, `tf`, `mc`, `multi` or `dropdown`. Default: `open`. |
| `a` | string | Yes for `open` | Model answer. |
| `html` | boolean | No | If `true`, the app keeps HTML in `q`, `ctx` and the options. Default: `false`. The model answer `a` always permits HTML. |
| `label` | string | No | Label such as `Part 1 (a)`. Default: `Q` + `n`. |
| `ctx` | string | No | Definitions for this question. The app shows them in a foldout. |
| `img`, `aImg` | string, array or object | No | Images for the question and the answer. Use a path, an array, or `{src, alt, caption}`. |
| `kw` | array of arrays | No | Keyword groups for **Type & match**. See "Keyword groups" below. |
| `mcq` | array of objects | No | Generated multiple-choice items for an `open` question. Each item has `q`, `a` (correct) and `w` (wrong answers). |

Add the fields below for the given `type`:

| `type` | Fields |
| --- | --- |
| `tf` | `answer`: `true` or `false`. |
| `mc` | `options`: at least two items. `correct`: one option index. |
| `multi` | `options`: at least two items. `correct`: array of option indexes. |
| `dropdown` | `blanks`: object. Each blank has `options` and `answer`. Put a `[[name]]` marker in `q` for each blank. |

An option is a string, or an object with `text` and `img`.

### Keyword groups

`kw` is an array of groups. Each group is an array of alternative spellings or
stems. The app gives one hit for each group that occurs in the typed answer. A
score of 60% or more counts as correct.

### Source text

`src` accepts these prefixes:

| Prefix | Shown as |
| --- | --- |
| `S-W4` | Slides · Week 4 |
| `T-W3` | Lecture transcript · Week 3 |
| `Tutorial` | Tutorial |
| `Canvas quiz` | Quiz |
| `Canvas assignment` | Assignment |

Separate several sources with `;`.

### Text and images

- Use `\( ... \)` or `\[ ... \]` for LaTeX. The app typesets it with KaTeX.
- Use a relative image path, an `http(s)` URL, or a `data:image` URI.
- To use the `images` map, set the image key as the `src` value. The app
  replaces the key with the data URI.

### Example

```json
{
  "title": "Example",
  "setLabel": "",
  "sets": ["Tute 1"],
  "questions": [
    {
      "id": "t1_q1",
      "set": "Tute 1",
      "n": 1,
      "q": "What is a process?",
      "a": "A program in execution.",
      "src": "S-W1"
    }
  ],
  "videos": {},
  "questionVideos": {}
}
```
