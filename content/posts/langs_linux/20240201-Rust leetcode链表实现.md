---
title: "Rust Leetcode链表实现"
date: 2024-02-01T14:00:40+08:00
lastmod: 2024-02-01T14:00:40+08:00
author: ["Reid"]
categories:
  - Rust
  - LinkedList
tags:
  - Option
  - Box
keyword:
  - Rust
  - LinkedList
description: Rust Leetcode链表实现
weight: # 输入1可以顶置文章，用来给文章展示排序，不填就默认按时间排序
slug: Rust leetcode链表实现
draft: false # 是否为草稿
comments: true
showToc: true # 显示目录
TocOpen: false # 自动展开目录
hidemeta: false # 是否隐藏文章的元信息，如发布日期、作者等
disableShare: true # 底部不显示分享栏
showbreadcrumbs: true #顶部显示当前路径
cover:
  image: ""
  caption: ""
  alt: ""
  relative: false
---

# Rust LinkedList 定义

Leetcode:
rust 如下:

```rust
// Definition for singly-linked list.
[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}

/// 单链表
#[derive(Debug)]
struct LinkedList<T> {
    head: Option<Box<Node<T>>>,
}

```

Go 如下:

```go
type ListNode struct {
     Val int
     Next *ListNode
 }

```

问题 1: 为什么 `Rust` 有`ListNode`之后还有`LinkedList` 定义?
与其他语言不通，`Rust` 中有所有权概念，在 Option<Box<LisNode>>的实现中，next 节点不存在引用类型，暗含的意思就是：链表头是整个链表的拥有者，负责整个链表所占据内存的管理（包括最终销）。进一步说，`Rust` 中这样实现的链表和用 C++实现的链表是完全不同的：每个节点不再是独立存在的了，而是被先驱节点所管理，同时也管理着它的 next 字段后所有的后驱节点。
问题 2: 为什么 next 是 `Option<Box<LisNode>>` 类型，而不是 ListNode？

- 节点的 next 指向下一个节点，可能为空，故类型为 Option；
- 避免编译器无法计算节点大小，用 Box 包裹 Node；
- next 实际上是用 Option 包裹的指向下个节点的 Box 指针，并且拥有下个节点的所有权；

## Box 的作用

在 `Rust` 中，`Box<T>` 是一个“箱子”类型，它在堆上存储数据。你可以把它看作是一个智能指针，用来封装和管理堆上的内存。

在这个 Node 结构体中，Box<Node> 是一个指向堆上的 Node 实例的指针。Option<Box<Node>> 则意味着这个指针可能有值（即 Some(Box(Node))），也可能没有值（即 None）。

以下是 `Box<T>` 在这个上下文中的一些主要用途：

- 递归数据结构：在定义递归或者链接的数据结构时，比如链表、树等，`Box<T>` 是必要的。在你的例子中，Node 结构体是一个链表节点，它有一个 next 字段指向下一个 Node。这个 next 字段需要使用 Box<Node>，因为 Rust 需要知道 Node 结构体的确切大小，而 Box<Node> 是一个固定大小的指针。
- 转移所有权：当你需要将值的所有权转移到其他函数或变量时，可以使用 `Box<T>`。`Box<T>` 拥有它所指向的值的所有权，当 `Box<T>` 被销毁时，它所指向的值也会被销毁。
- 大对象和内存管理：如果你有一个很大的对象或者需要手动管理内存，`Box<T>` 是一个很好的工具。因为 `Box<T>` 在堆上分配内存，当你不再需要这个值时，`Box<T>` 会自动回收它所使用的内存。

以上就是 `Box<T>` 的一些主要用途。在你的例子中，`Box<T>` 主要用于定义递归的链表数据结构。

## 不使用 Box 可行？

在定义递归数据结构时，如链表或树，`Rust` 语言要求必须使用 Box 或者其他形式的间接寻址（如 Rc、Arc 等）。这是由 `Rust` 的所有权和内存安全性规则决定的。

`Rust` 编译器需要在编译时就知道每种类型的确切大小。对于递归类型，例如链表节点 Node，如果不使用 Box 或其他形式的指针，Node 类型会有一个无限的大小。这是因为每个 Node 都包含另一个 Node，这形成了一个无限的嵌套。这会导致编译时错误，因为 `Rust` 无法确定类型的确切大小。

Box（以及 Rc、Arc 等）是一个固定大小的指针类型，它在堆上存储数据。这意味着，对于 Box<Node> 类型，无论 Node 的实际大小如何，Box<Node> 类型总是有一个固定的大小。这使得在 `Rust` 中定义递归类型成为可能。

所以，对于你的例子，如果你要在 Node 中定义一个指向另一个 Node 的字段，你必须使用 Box 或其他形式的指针。否则，你会得到一个编译错误。

## 和 Rc<RefCell<T>> 的区别

`Box` 和 `Rc<RefCell<T>>` 都是 `Rust` 中的智能指针类型，但是它们的用途和行为不同。

`Box<T>` 提供了在堆上分配一个值的能力，并拥有这个值的所有权。当 `Box` 被丢弃（drop）时，它包含的值也会被丢弃。`Box` 只有一个所有者。
Rc<T> 是一个引用计数类型，可以让一个值有多个所有者。每当你克隆一个 Rc 指针，引用计数就会增加。当一个 Rc 指针被丢弃时，引用计数就会减少。只有当引用计数为 0 时，值才会被丢弃。
RefCell<T> 提供了内部可变性。在 Rust 中，我们不能同时拥有一个值的可变引用和不可变引用。然而，有时我们可能需要在运行时改变一个值，即使我们拥有的是一个不可变引用。这就是 RefCell 发挥作用的地方。RefCell 允许我们在运行时借用和改变值，但是如果我们违反了借用规则（例如，同时拥有可变引用和不可变引用），RefCell 就会导致程序 panic。
当你看到 Option<Rc<RefCell<TreeNode>>> 时，这是因为在一些情况下（例如，在树或图结构中），我们需要一个节点有多个所有者，或者我们需要修改一个被多个地方引用的值。在这种情况下，我们就需要使用 Rc 和 RefCell。

然而，请注意，Rc<RefCell<T>> 在运行时执行借用检查，可能会引发 panic，而且引用计数会增加运行时开销。在可以确定一个值只有一个所有者，并且不需要在运行时修改的情况下，使用 `Box<T>` 会更简单、更安全、更高效。

# 反转链表实现

```rust
pub fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut prev = None;
    let mut cur = head;

    while let Some(mut node) = cur {
        let next = node.next;
        node.next = prev;

        cur = next;
        prev = Some(node);
    }

    prev
}

let mut list = ListNode::new(1);
        list.next = Some(Box::new(ListNode::new(2)));
        list.next.as_mut().unwrap().next = Some(Box::new(ListNode::new(3)));
        list.next.as_mut().unwrap().next.as_mut().unwrap().next = Some(Box::new(ListNode::new(4)));
        list.next
            .as_mut()
            .unwrap()
            .next
            .as_mut()
            .unwrap()
            .next
            .as_mut()
            .unwrap()
            .next = Some(Box::new(ListNode::new(5)));
        let reversed_list = reverse_linked_list(Option::from(Box::from(list)));
        assert_eq!(reversed_list.as_ref().unwrap().value, 5);
        assert_eq!(
            reversed_list.as_ref().unwrap().next.as_ref().unwrap().value,
            4
        );
```

## as_mut().unwrap()，.as_ref().unwrap() 的作用

在 Rust 中，.as_mut() 和 .as_ref() 方法通常被用来转换 Option 或 Result 类型。

- .as_mut() 是 Option 和 Result 类型的一个方法，用来将 Option<T> 或 Result<T, E> 转换成 Option<&mut T> 或 Result<&mut T, &mut E>。也就是说，它返回一个包含可变引用的新的 Option 或 Result。
- .unwrap() 是 Option 和 Result 类型的一个方法，用来获取它们包含的值。如果 Option 是 Some(v)，它返回 v，如果 Option 是 None，它会 panic（意味着程序会立即停止，并给出一个错误信息）。对于 Result，如果它是 Ok(v)，它返回 v，如果它是 Err(e)，它也会 panic。
- .as_ref() 是 Option 和 Result 类型的一个方法，用来将 Option<T> 或 Result<T, E> 转换成 Option<&T> 或 Result<&T, &E>。也就是说，它返回一个包含不可变引用的新的 Option 或 Result。

- as_mut().unwrap() 和 as_ref().unwrap() 都被用来获取 Option<Box<Node>> 中的 Node。这样，你就可以修改或访问 Node 中的 value 和 next。因为 Option<Box<Node>> 中可能没有 Node（也就是它可能是 None），所以需要使用 unwrap() 来获取 Node。但是请注意，如果 Option<Box<Node>> 是 None，unwrap() 会引发 panic。为了避免这种情况，你需要在调用 unwrap() 之前确保 Option 不是 None。

## unwrap() 不能调用多次，其实是所有权问题

你遇到的这个错误是由于在 Rust 中的所有权规则所引起的。当你对 Option 类型的值调用 unwrap() 方法时，它会获取 Option 的所有权，这意味着原来的 Option 值将不能再使用。

这就是为什么你在 while 循环中多次使用 head.unwrap().next 时会遇到问题。在第一次调用 unwrap() 之后，head 就被移动（move）了，也就是说它的所有权被转移走了，所以你不能再次对 head 调用 unwrap()。

## Option::from 和 Some 是一样的？

是的，你完全正确。在 Rust 中，Some(value) 和 Option::from(value) 是等价的。它们都会创建一个包含 value 的 Option 枚举值。

Some(value) 是更常见的使用方式，它直接创建了一个 Option::Some 枚举变量。例如：3

```rust
let some_number = Some(5);
```

Option::from(value) 是 From trait 的一部分，这个 trait 用于定义如何将一种类型转换成另一种类型。Option::from 的定义如下：

```rust
impl<T> From<T> for Option<T> {
    fn from(value: T) -> Option<T> {
        Some(value)
    }
}
```

因此，Option::from(value) 实际上就是返回 Some(value)。例如：

```rust
let some_number = Option::from(5);
```

在大多数情况下，直接使用 Some(value) 会更简单和直观。

## take 函数

```rust
let mut x = Some(2);
let y = x.take();
assert_eq!(x, None);
assert_eq!(y, Some(2));
```

这段代码中的 x.take() 方法是 Option 类型特有的方法。take() 方法将 Option 置为 None 并返回原来的值。

当你调用 x.take() 时，它会把 x 里面的值取出并返回，此时 x 的值就变为了 None，因为你已经取走了它的值。所以，在 x.take() 后，x 的值就是 None 了。

而 y 的值是 x.take() 的返回值，即 x 原来的值 Some(2)，所以 y 的值就是 Some(2)。

简单地说，x.take() 做了两件事：

将 x 设为 None。
返回 x 原来的值。
因此，x 在调用 take 之后的值是 None，而 y 的值就是 x 在调用 take 之前的值，即 Some(2)。

这就是为什么在 assert_eq!(x, None) 和 assert_eq!(y, Some(2)) 的断言语句都能通过，因为它们分别测试的是 x 和 y 的值，这些值都符合预期。
