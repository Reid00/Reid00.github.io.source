package main

import (
	"flag"
	"fmt"
	"os/exec"
	"time"
)

func main() {
	var kind, name string
	var folder string

	flag.StringVar(&name, "n", "", "post file name")
	flag.StringVar(&kind, "k", "default", "post template")
	flag.StringVar(&folder, "f", "posts", "markdown parent folder name")

	flag.Parse()
	fmt.Printf("kind is %s, name is %s, folder name: %s\n", kind, name, folder)
	fmt.Println("====================================")

	date := time.Now().Format("20060102")

	fileName := date + "-" + name + ".md"

	cmd := fmt.Sprintf("%s/%s", folder, fileName)

	fmt.Println("new post command is: ", cmd)

	command := exec.Command("hugo", "new", "-k", kind, cmd)
	err := command.Run()
	if err != nil {
		panic(err)
	}
}
