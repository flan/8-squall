package structure
import (
    "github.com/juju/loggo"
    "math/rand"
    "time"
)

var logger = loggo.GetLogger("core_stats")

const rescaleThreshold int = 65000

var rng := rand.Rand.New(rand.NewSource(time.Now().Unix()))
