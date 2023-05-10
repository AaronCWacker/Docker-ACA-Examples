FROM golang:1.18 as builder

WORKDIR /workdir

COPY main.go .

RUN go build -o main main.go

FROM golang:1.18
WORKDIR /workdir

COPY --from=builder /workdir/main /main
CMD /main
